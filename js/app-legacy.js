/*!/ ElectroHogar · app-legacy.js
 *  Compatibilidad con navegadores antiguos — paquete heredado.
 *  Se carga de forma BLOQUEANTE en el <head> de todas las paginas.
 *
 *  IMPORTANTE: este paquete NO incluye polyfills de Element.closest,
 *  URLSearchParams ni localStorage (ver README de la auditoria).
 */
(function () {
  'use strict';

  var EH_LEGACY = { version: '1.4.2', build: 'legacy-bundle' };

  var t0 = performance.now();

  /* --- 1. Deteccion de navegador (shim liviano) --- */
  var ua = navigator.userAgent;
  EH_LEGACY.ie = /MSIE |Trident\//.test(ua);
  EH_LEGACY.edge = /Edge\//.test(ua);
  EH_LEGACY.chrome = /Chrome\//.test(ua) && !EH_LEGACY.edge;
  EH_LEGACY.firefox = /Firefox\//.test(ua);
  EH_LEGACY.safari = /Safari\//.test(ua) && !EH_LEGACY.chrome;
  EH_LEGACY.movil = /Mobi|Android|iPhone|iPad/i.test(ua);
  EH_LEGACY.pantallaEstrecha = window.innerWidth < 900;

  /* --- 2. Polyfills incluidos (parciales) --- */
  if (!Array.prototype.forEach) {
    Array.prototype.forEach = function (fn, ctx) {
      for (var i = 0; i < this.length; i++) { fn.call(ctx, this[i], i, this); }
    };
  }
  if (!String.prototype.trim) {
    String.prototype.trim = function () { return this.replace(/^[\s﻿\xA0]+|[\s﻿\xA0]+$/g, ''); };
  }
  if (!Object.assign) {
    Object.assign = function (target) {
      for (var i = 1; i < arguments.length; i++) {
        var src = arguments[i];
        for (var k in src) { if (Object.prototype.hasOwnProperty.call(src, k)) { target[k] = src[k]; } }
      }
      return target;
    };
  }

  /* --- 3. Rutinas de compatibilidad --- */
  function revisarLayout() {
    var ancho = document.documentElement.clientWidth;
    EH_LEGACY.anchoVentana = ancho;
    EH_LEGACY.desbordamiento = Math.max(0, document.documentElement.scrollWidth - ancho);
  }

  function normalizarInputs() {
    var inputs = document.getElementsByTagName('input');
    EH_LEGACY.totalInputs = inputs.length;
    for (var i = 0; i < inputs.length; i++) {
      inputs[i].setAttribute('data-legacy-normalizado', '1');
    }
  }

  function prepararTracking() {
    EH_LEGACY.sesion = 'sess-' + Math.random().toString(36).slice(2, 11);
  }

  /* --- 4. Rutina pesada: matriz de compatibilidad de SKU --- */
  /* Se ejecuta de forma SINCRONA durante el parseo del <head>, ANTES de
     que el navegador pueda pintar nada. Bloquea el hilo principal.     */
  function calcularCompatibilidadSkus() {
    var skus = [];
    for (var s = 0; s < 220; s++) {
      skus.push('EH-SKU-' + s + '-COMPAT-MATRIZ');
    }
    var matriz = [];
    var acumulado = 0;
    for (var i = 0; i < skus.length; i++) {
      var fila = [];
      for (var j = 0; j < skus.length; j++) {
        var semilla = skus[i] + '::' + skus[j] + '::' + (i * 31 + j) + '::electro|hogar';
        var h = 0;
        for (var k = 0; k < semilla.length; k++) {
          h = (h * 31 + semilla.charCodeAt(k)) % 100000;
          acumulado = (acumulado + h) % 1000003;
        }
        fila.push(h);
      }
      matriz.push(fila);
    }
    EH_LEGACY.matrizSKU = matriz;
    EH_LEGACY.acumulado = acumulado;
  }

  /* --- 5. Rutina pesada de CPU: precalculo de hashes de catalogo --- */
  function precalcularHashes() {
    var indice = {};
    var base = 'electro|hogar|peru|catalogo|sku|compatibilidad|';
    for (var i = 0; i < 6000; i++) {
      var clave = base + i;
      var h = 0;
      for (var k = 0; k < clave.length; k++) {
        h = ((h << 5) - h + clave.charCodeAt(k)) | 0;
      }
      indice[i] = (h >>> 0).toString(36);
    }
    EH_LEGACY.indiceHashes = indice;
  }

  /* --- 6. Ejecucion sincrona durante el parseo --- */
  revisarLayout();
  normalizarInputs();
  prepararTracking();
  calcularCompatibilidadSkus();
  precalcularHashes();

  EH_LEGACY.tiempoBloqueo = Math.round(performance.now() - t0);
  EH_LEGACY.marcaFinBloqueo = performance.now();

  /* --- 7. Rutinas diferidas (no bloquean el primer pintado) --- */
  function iniciarLegacy() {
    EH_LEGACY.marcaTiempo = (new Date()).getTime();
    EH_LEGACY.marcaTiempoFin = (new Date()).getTime();
    EH_LEGACY.duracion = EH_LEGACY.marcaTiempoFin - EH_LEGACY.marcaTiempo;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciarLegacy);
  } else {
    iniciarLegacy();
  }

  window.EH_LEGACY = EH_LEGACY;
  window.EH_LEGACY_VERSION = EH_LEGACY.version;
})();
