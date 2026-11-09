"""Extractor etico: respeta robots.txt, se identifica y no satura sitios.

Basado en el codigo del Kit de arranque del Trusted Data Lab.
Cambia CONTACTO por el correo del equipo antes de la primera captura.
"""

from __future__ import annotations

import time
import urllib.robotparser
from urllib.parse import urlparse

import requests

CONTACTO = "22460314@colima.tecnm.mx"
UA = f"TDL-Observatorio/1.0 (proyecto academico TecNM Colima; contacto: {CONTACTO})"


class ExtractorEtico:
    """Cliente HTTP que respeta robots.txt, Crawl-delay y una pausa minima por dominio."""

    def __init__(self, pausa: float = 1.5, timeout: int = 60):
        self.pausa = pausa  # segundos minimos entre peticiones al mismo dominio
        self.timeout = timeout
        self.robots: dict[str, urllib.robotparser.RobotFileParser] = {}
        self.ultimo: dict[str, float] = {}
        self.sesion = requests.Session()
        self.sesion.headers["User-Agent"] = UA

    def _reglas(self, url: str) -> urllib.robotparser.RobotFileParser:
        p = urlparse(url)
        base = f"{p.scheme}://{p.netloc}"
        if base not in self.robots:
            rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
            try:
                r = self.sesion.get(base + "/robots.txt", timeout=self.timeout)
                lineas = r.text.splitlines() if r.status_code == 200 else []
            except requests.RequestException:
                lineas = []
            rp.parse(lineas)  # sin robots.txt = todo permitido (RFC 9309)
            self.robots[base] = rp
        return self.robots[base]

    def permitido(self, url: str) -> bool:
        return self._reglas(url).can_fetch(UA, url)

    def get(self, url: str, params: dict | None = None, intentos: int = 3, api: bool = False) -> requests.Response:
        """Descarga respetando robots.txt.

        api=True solo para APIs oficiales y documentadas (Open-Meteo, CRE, INEGI): su robots.txt
        suele prohibir el *rastreo* (Disallow: /), pero el acceso programatico se rige por sus
        terminos de uso, que se documentan en docs/E0/propuesta.md. Se mantienen el User-Agent
        y la pausa entre peticiones.
        """
        reglas = self._reglas(url)
        if not api and not reglas.can_fetch(UA, url):
            raise PermissionError(f"robots.txt no permite {url}")
        dominio = urlparse(url).netloc
        pausa = max(self.pausa, reglas.crawl_delay(UA) or 0)
        ultimo_error: Exception | None = None
        for i in range(intentos):
            espera = pausa - (time.time() - self.ultimo.get(dominio, 0))
            if espera > 0:
                time.sleep(espera)
            try:
                r = self.sesion.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as e:  # red caida, timeout
                ultimo_error = e
                self.ultimo[dominio] = time.time()
                time.sleep(pausa * 2**i)
                continue
            self.ultimo[dominio] = time.time()
            if r.status_code == 429 or r.status_code >= 500:
                ultimo_error = RuntimeError(f"HTTP {r.status_code}")
                time.sleep(pausa * 2**i)  # espera exponencial ante saturacion
                continue
            r.raise_for_status()
            return r
        raise RuntimeError(f"Sin respuesta valida de {url} tras {intentos} intentos: {ultimo_error}")
