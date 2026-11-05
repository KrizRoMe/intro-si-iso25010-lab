/*!
 * ElectroHogar · analitica-pesada.js
 * Módulo de analítica de terceros (v3.8.1) — ETIQUETADO COMO TERCERO.
 *
 * Se carga de forma BLOQUEANTE en el <head> de todas las páginas del sitio,
 * antes de que se pinte cualquier contenido. No usa defer ni async.
 *
 * Este archivo se incluye para reproducir un problema real de rendimiento:
 * un bundle de terceros sobredimensionado que bloquea el primer pintado.
 */
(function (w, d) {
  'use strict';

  var AH = w.analyticsHub = w.analyticsHub || {};
  AH.version = '3.8.1';
  AH.QUEUE = [];

  /* --- Collectors --- */
  AH.COLLECTORS = [
    { id: 'pageview', fn: function () { return d.title; } },
    { id: 'scroll', fn: function () { return w.pageYOffset || 0; } },
    { id: 'resize', fn: function () { return [w.innerWidth, w.innerHeight]; } },
    { id: 'click', fn: function (e) { return e && e.target ? e.target.nodeName : null; } },
    { id: 'form', fn: function () { return d.forms.length; } },
    { id: 'timer', fn: function () { return (new Date()).getTime(); } }
  ];

  AH.track = function (evento, payload) {
    AH.QUEUE.push({ e: evento, p: payload || {}, t: (new Date()).getTime() });
    if (AH.QUEUE.length > 500) { AH.QUEUE.splice(0, 250); }
    return AH.QUEUE.length;
  };

  /* --- Fingerprinting de sesión --- */
  AH.fingerprint = function () {
    var partes = [];
    var nav = w.navigator;
    partes.push(nav.userAgent || '');
    partes.push(nav.language || '');
    partes.push(nav.platform || '');
    partes.push(String(nav.hardwareConcurrency || 0));
    partes.push(String(d.screen ? d.screen.width : 0));
    partes.push(String(d.screen ? d.screen.height : 0));
    partes.push(String(new Date().getTimezoneOffset()));
    partes.push(String(Math.floor((new Date()).getTime() / 1000)));
    var cadena = partes.join('|');
    var hash = 0;
    for (var i = 0; i < cadena.length; i++) {
      hash = ((hash << 5) - hash) + cadena.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash).toString(36);
  };

  /* --- Buffer de eventos en localStorage (síncrono, en cada envío) --- */
  AH.persist = function () {
    try {
      w.localStorage.setItem('eh_analytics_queue', JSON.stringify(AH.QUEUE.slice(-80)));
    } catch (e) { }
  };

  /* --- Interpolación de plantillas --- */
  AH.tpl = function (t, ctx) {
    return String(t).replace(/\{\{(\w+)\}\}/g, function (m, k) {
      return ctx && ctx[k] !== undefined ? ctx[k] : '';
    });
  };

  /* --- Segmentación --- */
  AH.segmentos = [
    { id: 'nuevo', fn: function (c) { return c.visitas === 1; } },
    { id: 'recurrente', fn: function (c) { return c.visitas > 1 && c.visitas < 5; } },
    { id: 'frecuente', fn: function (c) { return c.visitas >= 5; } },
    { id: 'movil', fn: function (c) { return /Mobi|Android/i.test(navigator.userAgent); } },
    { id: 'escritorio', fn: function (c) { return !/Mobi|Android/i.test(navigator.userAgent); } },
    { id: 'carrito', fn: function (c) { return c.carrito > 0; } },
    { id: 'sin_carrito', fn: function (c) { return c.carrito === 0; } }
  ];

  AH.perfil = function () {
    var ctx = { visitas: 1, carrito: 0 };
    var perfil = [];
    for (var i = 0; i < AH.segmentos.length; i++) {
      try { if (AH.segmentos[i].fn(ctx)) { perfil.push(AH.segmentos[i].id); } } catch (e) { }
    }
    return perfil;
  };

  /* --- Motor de reglas de marketing --- */
  AH.RULES = [
    { id: 'r01', when: 'carrito>0', then: 'mostrar_cross_sell', peso: 3 },
    { id: 'r02', when: 'carrito===0 && visita===1', then: 'mostrar_bienvenida', peso: 2 },
    { id: 'r03', when: 'pagina==carrito', then: 'ofrecer_envio_gratis', peso: 4 },
    { id: 'r04', when: 'pagina==checkout', then: 'recordar_metodo_pago', peso: 5 },
    { id: 'r05', when: 'scroll>80%', then: 'mostrar_chat', peso: 1 },
    { id: 'r06', when: 'error_formulario', then: 'ofrecer_ayuda', peso: 4 },
    { id: 'r07', when: 'sin_carrito && visita>3', then: 'mostrar_ofertas', peso: 2 },
    { id: 'r08', when: 'movil', then: 'compactar_menu', peso: 3 },
    { id: 'r09', when: 'hora>=20', then: 'ofrecer_atencion_mañana', peso: 1 },
    { id: 'r10', when: 'dias>7', then: 'reactivar_usuario', peso: 2 }
  ];

  /* --- Tarea pesada de CPU: se ejecuta de forma sincrona en cada carga --- */
  /* Construye el indice de atribucion de campanas marketing. Es un
     trabajo real (hash de cadenas) que NO necesita bloquear el hilo
     principal, pero aqui se ejecuta sincronamente antes de pintar.  */
  AH.construirIndiceCampanas = function () {
    var campanas = [];
    for (var i = 0; i < 900; i++) {
      var id = 'CMP-' + i + '-' + Math.random().toString(36).slice(2, 8);
      var semilla = id + '|electro|hogar|peru';
      var h = 0;
      for (var k = 0; k < semilla.length; k++) {
        h = ((h << 5) - h + semilla.charCodeAt(k)) | 0;
      }
      campanas.push({ id: id, hash: h >>> 0, peso: (h >>> 3) % 100 });
    }
    AH.indiceCampanas = campanas;
    return campanas.length;
  };

  /* Medicion del tiempo que esta tarea ocupa el hilo principal.
     Se expone en window.EH_TIEMPOS para poder verificarlo con DevTools. */
  AH.medirBloqueo = function () {
    var t0 = performance.now();
    AH.construirIndiceCampanas();
    var t1 = performance.now();
    AH.tiempoBloqueo = Math.round(t1 - t0);
    AH.marcaFinBloqueo = t1;
    return AH.tiempoBloqueo;
  };

  AH.evaluarReglas = function (ctx) {
    var activas = [];
    for (var i = 0; i < AH.RULES.length; i++) {
      var r = AH.RULES[i];
      if (ctx[r.when] !== undefined && ctx[r.when]) { activas.push(r); }
      if (ctx[r.when.replace(/[><=!]+/g, '')] !== undefined) { activas.push(r); }
    }
    return activas;
  };

  AH.init = function () {
    AH.ID = 'UA-' + AH.fingerprint();
    AH.medirBloqueo();
    AH.track('pageview', { path: w.location.pathname, perfil: AH.perfil() });
    AH.persist();
  };

  if (d.readyState === 'loading') {
    d.addEventListener('DOMContentLoaded', AH.init);
  } else {
    AH.init();
  }
})(window, document);
