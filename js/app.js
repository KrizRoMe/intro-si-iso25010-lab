/* ElectroHogar · lógica del sitio */
var CARRITO = [];
var LLAVE = 'eh_carrito_v1';

function leerCarrito() {
  try {
    var dato = window.localStorage.getItem(LLAVE);
    CARRITO = dato ? JSON.parse(dato) : [];
  } catch (e) {
    CARRITO = [];
  }
}

function guardarCarrito() {
  try {
    window.localStorage.setItem(LLAVE, JSON.stringify(CARRITO));
  } catch (e) { }
}

function refrescarContador() {
  var nodo = document.getElementById('contador-carrito');
  if (nodo) { nodo.textContent = String(CARRITO.length); }
}

function totalCarrito() {
  var total = 0;
  for (var i = 0; i < CARRITO.length; i++) {
    total = total + CARRITO[i].precio;
  }
  return total;
}

function unidadesTotales() {
  var n = 0;
  for (var i = 0; i < CARRITO.length; i++) { n = n + (CARRITO[i].cantidad || 1); }
  return n;
}

function agregarAlCarrito(idProducto) {
  var producto = null;
  for (var i = 0; i < PRODUCTOS.length; i++) {
    if (PRODUCTOS[i].id === Number(idProducto)) { producto = PRODUCTOS[i]; break; }
  }
  if (!producto) { return; }
  var existente = null;
  for (var j = 0; j < CARRITO.length; j++) {
    if (CARRITO[j].id === producto.id) { existente = CARRITO[j]; break; }
  }
  if (existente) {
    existente.cantidad = existente.cantidad + 1;
  } else {
    CARRITO.push({
      id: producto.id,
      nombre: producto.nombre,
      marca: producto.marca,
      precio: producto.precio,
      imagen: producto.imagen,
      cantidad: 1
    });
  }
  guardarCarrito();
}

function quitarDelCarrito(idProducto) {
  var nueva = [];
  for (var i = 0; i < CARRITO.length; i++) {
    if (CARRITO[i].id !== Number(idProducto)) { nueva.push(CARRITO[i]); }
  }
  CARRITO = nueva;
  guardarCarrito();
}

function cambiarCantidad(idProducto, delta) {
  for (var i = 0; i < CARRITO.length; i++) {
    if (CARRITO[i].id === Number(idProducto)) {
      CARRITO[i].cantidad = CARRITO[i].cantidad + delta;
      if (CARRITO[i].cantidad < 1) { CARRITO[i].cantidad = 1; }
    }
  }
  guardarCarrito();
}

function pintarOpcionesCategoria() {
  var sel = document.getElementById('filtro-categoria');
  if (!sel) { return; }
  for (var i = 0; i < CATEGORIAS.length; i++) {
    var op = document.createElement('option');
    op.value = CATEGORIAS[i];
    op.textContent = CATEGORIAS[i];
    sel.appendChild(op);
  }
}

function filtrarProductos() {
  var lista = PRODUCTOS.slice();

  var selCat = document.getElementById('filtro-categoria');
  if (selCat && selCat.value) {
    lista = lista.filter(function (p) { return p.categoria === selCat.value; });
  }

  var desde = document.getElementById('precio-desde');
  var hasta = document.getElementById('precio-hasta');
  var d = desde && desde.value !== '' ? parseFloat(desde.value) : null;
  var h = hasta && hasta.value !== '' ? parseFloat(hasta.value) : null;

  if (d !== null && h !== null) {
    lista = lista.filter(function (p) { return !(p.precio >= d && p.precio <= h); });
  } else if (d !== null) {
    lista = lista.filter(function (p) { return p.precio < d; });
  } else if (h !== null) {
    lista = lista.filter(function (p) { return p.precio > h; });
  }

  var selOrd = document.getElementById('orden');
  if (selOrd) {
    var v = selOrd.value;
    if (v === 'precio-asc') {
      lista.sort(function (a, b) { return a.precio - b.precio; });
    } else if (v === 'precio-desc') {
      lista.sort(function (a, b) { return b.precio - a.precio; });
    } else if (v === 'nombre') {
      lista.sort(function (a, b) { return a.nombre.localeCompare(b.nombre, 'es'); });
    }
  }
  return lista;
}

function pintarCatalogo() {
  var rejilla = document.getElementById('rejilla');
  if (!rejilla) { return; }
  var lista = filtrarProductos();
  rejilla.innerHTML = '';

  if (lista.length === 0) {
    var vacio = document.createElement('div');
    vacio.className = 'vacio';
    vacio.setAttribute('style', 'grid-column: 1 / -1;');
    vacio.textContent = 'No se encontraron productos con esos criterios.';
    rejilla.appendChild(vacio);
    return;
  }

  for (var i = 0; i < lista.length; i++) {
    var p = lista[i];
    var tarjeta = document.createElement('article');
    tarjeta.className = 'tarjeta';

    var enlace = document.createElement('a');
    enlace.href = 'producto.html?id=' + p.id;
    var img = document.createElement('img');
    img.className = 'tarjeta-img';
    img.src = p.imagen;
    img.alt = p.nombre;
    enlace.appendChild(img);

    var cuerpo = document.createElement('div');
    cuerpo.className = 'tarjeta-body';

    var marca = document.createElement('p');
    marca.className = 'tarjeta-marca';
    marca.textContent = p.marca.toUpperCase();
    cuerpo.appendChild(marca);

    var titulo = document.createElement('h3');
    titulo.className = 'tarjeta-titulo';
    var tEnlace = document.createElement('a');
    tEnlace.href = 'producto.html?id=' + p.id;
    tEnlace.style.color = 'inherit';
    tEnlace.style.textDecoration = 'none';
    tEnlace.textContent = p.nombre;
    titulo.appendChild(tEnlace);
    cuerpo.appendChild(titulo);

    var lineaPrecio = document.createElement('div');
    lineaPrecio.className = 'tarjeta-precio';
    var precio = document.createElement('span');
    precio.className = 'precio';
    precio.textContent = 'S/ ' + p.precio.toFixed(2);
    lineaPrecio.appendChild(precio);
    if (p.precioAntes) {
      var antes = document.createElement('span');
      antes.className = 'precio-antes';
      antes.textContent = 'S/ ' + p.precioAntes.toFixed(2);
      lineaPrecio.appendChild(antes);
    }
    cuerpo.appendChild(lineaPrecio);

    var stock = document.createElement('p');
    stock.className = 'ayuda';
    stock.textContent = 'Stock: ' + p.stock + ' unidades';
    cuerpo.appendChild(stock);

    var btn = document.createElement('button');
    btn.className = 'btn btn-primario btn-bloque';
    btn.type = 'button';
    btn.textContent = 'Agregar al carrito';
    btn.setAttribute('data-id', String(p.id));
    cuerpo.appendChild(btn);

    tarjeta.appendChild(enlace);
    tarjeta.appendChild(cuerpo);
    rejilla.appendChild(tarjeta);
  }
}

function conectarCatalogo() {
  var botonBuscar = document.getElementById('q-busqueda');
  if (botonBuscar) {
    botonBuscar.addEventListener('input', function () {
      var texto = botonBuscar.value.toLowerCase().trim();
      pintarCatalogo();
      var tarjetas = document.querySelectorAll('.tarjeta');
      for (var i = 0; i < tarjetas.length; i++) {
        var coincide = tarjetas[i].textContent.toLowerCase().indexOf(texto) !== -1;
        tarjetas[i].style.display = coincide ? '' : 'none';
      }
    });
  }

  var selCat = document.getElementById('filtro-categoria');
  if (selCat) { selCat.addEventListener('change', pintarCatalogo); }

  var selOrd = document.getElementById('orden');
  if (selOrd) { selOrd.addEventListener('change', pintarCatalogo); }

  var desde = document.getElementById('precio-desde');
  if (desde) { desde.addEventListener('input', pintarCatalogo); }

  var hasta = document.getElementById('precio-hasta');
  if (hasta) { hasta.addEventListener('input', pintarCatalogo); }

  var rejilla = document.getElementById('rejilla');
  if (rejilla) {
    rejilla.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button[data-id]');
      if (!btn) { return; }
      agregarAlCarrito(btn.getAttribute('data-id'));
    });
  }
}

function pintarResumen() {
  var total = totalCarrito();
  var nArt = document.getElementById('num-articulos');
  if (nArt) { nArt.textContent = String(unidadesTotales()); }
  var nLineas = document.getElementById('num-lineas');
  if (nLineas) { nLineas.textContent = String(CARRITO.length); }
  var totalNodo = document.getElementById('total-general');
  if (totalNodo) { totalNodo.textContent = 'S/ ' + total.toFixed(2); }
  var envio = document.getElementById('costo-envio');
  if (envio) { envio.textContent = total >= 200 ? 'S/ 0.00' : 'S/ 15.00'; }
  var sub = document.getElementById('subtotal');
  if (sub) { sub.textContent = 'S/ ' + total.toFixed(2); }
}

function pintarCarrito() {
  pintarResumen();
  var contenedor = document.getElementById('filas-carrito');
  if (!contenedor) { return; }
  contenedor.innerHTML = '';

  if (CARRITO.length === 0) {
    var vacio = document.createElement('div');
    vacio.className = 'carrito-vacio';
    vacio.innerHTML = '<p>Tu carrito está vacío.</p><a class="btn btn-primario" href="index.html#catalogo">Ir al catálogo</a>';
    contenedor.appendChild(vacio);
    var panel = document.getElementById('panel-resumen');
    if (panel) { panel.style.display = 'none'; }
    return;
  }

  for (var i = 0; i < CARRITO.length; i++) {
    var it = CARRITO[i];
    var fila = document.createElement('div');
    fila.className = 'fila-carrito';

    var img = document.createElement('img');
    img.src = it.imagen;
    img.alt = it.nombre;
    fila.appendChild(img);

    var info = document.createElement('div');
    info.className = 'fila-info';
    var h = document.createElement('h3');
    h.textContent = it.nombre;
    info.appendChild(h);
    var meta = document.createElement('p');
    meta.textContent = it.marca + ' · Cantidad: ' + (it.cantidad || 1);
    info.appendChild(meta);

    var ctrl = document.createElement('div');
    ctrl.className = 'controles-cantidad';
    var menos = document.createElement('button');
    menos.type = 'button';
    menos.className = 'btn-secundario btn-menos';
    menos.textContent = '-';
    menos.setAttribute('data-id', String(it.id));
    menos.setAttribute('data-delta', '-1');
    var mas = document.createElement('button');
    mas.type = 'button';
    mas.className = 'btn-secundario btn-mas';
    mas.textContent = '+';
    mas.setAttribute('data-id', String(it.id));
    mas.setAttribute('data-delta', '1');
    ctrl.appendChild(menos);
    ctrl.appendChild(mas);
    info.appendChild(ctrl);

    fila.appendChild(info);

    var precio = document.createElement('div');
    precio.className = 'fila-precio';
    precio.textContent = 'S/ ' + it.precio.toFixed(2);
    fila.appendChild(precio);

    var quitar = document.createElement('button');
    quitar.type = 'button';
    quitar.className = 'btn-quitar';
    quitar.textContent = '\u00d7';
    quitar.setAttribute('data-quitar', String(it.id));
    fila.appendChild(quitar);

    contenedor.appendChild(fila);
  }

  pintarResumen();
}

function conectarCarrito() {
  var contenedor = document.getElementById('filas-carrito');
  if (!contenedor) { return; }
  contenedor.addEventListener('click', function (ev) {
    var btnQuitar = ev.target.closest('[data-quitar]');
    if (btnQuitar) {
      quitarDelCarrito(btnQuitar.getAttribute('data-quitar'));
      pintarCarrito();
      refrescarContador();
      return;
    }
    var btnMas = ev.target.closest('[data-delta]');
    if (btnMas) {
      cambiarCantidad(btnMas.getAttribute('data-id'), parseInt(btnMas.getAttribute('data-delta'), 10));
      pintarCarrito();
    }
  });
}

function conectarCheckout() {
  var form = document.getElementById('form-pago');
  if (!form) { return; }

  var aviso = document.getElementById('aviso-form');
  var ok = document.getElementById('aviso-ok');
  var panel = document.getElementById('form-panel');

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (ok) { ok.style.display = 'none'; }
    if (panel) { panel.style.display = ''; }

    var campos = form.querySelectorAll('input[required], select[required]');
    var faltan = [];
    for (var i = 0; i < campos.length; i++) {
      if (!campos[i].value.trim()) { faltan.push(campos[i].id); }
    }

    if (faltan.length > 0) {
      if (aviso) {
        aviso.className = 'aviso aviso-error';
        aviso.style.display = 'block';
        aviso.textContent = 'Datos inválidos. Revisa el formulario.';
      }
      return;
    }
    if (aviso) { aviso.style.display = 'none'; }
    if (panel) { panel.style.display = 'none'; }
    if (ok) {
      ok.className = 'aviso aviso-ok';
      ok.style.display = 'block';
      ok.innerHTML = '<strong>Pedido confirmado.</strong> N&uacute;mero de pedido EH-2026-004312. Te enviamos el detalle a tu correo.';
    }
  });
}

function conectarCuenta() {
  var pestanas = document.querySelectorAll('.pestanas button');
  if (!pestanas.length) { return; }
  for (var i = 0; i < pestanas.length; i++) {
    pestanas[i].addEventListener('click', function () {
      for (var j = 0; j < pestanas.length; j++) { pestanas[j].classList.remove('activa'); }
      this.classList.add('activa');
      var esLogin = this.getAttribute('data-panel') === 'login';
      var pLogin = document.getElementById('panel-login');
      var pRegistro = document.getElementById('panel-registro');
      if (pLogin) { pLogin.style.display = esLogin ? '' : 'none'; }
      if (pRegistro) { pRegistro.style.display = esLogin ? 'none' : ''; }
    });
  }
}

function conectarCookies() {
  var banner = document.getElementById('banner-cookies');
  if (!banner) { return; }
  var btnSi = document.getElementById('btn-cookies-si');
  var btnNo = document.getElementById('btn-cookies-no');
  function cerrar() { banner.style.display = 'none'; }
  if (btnSi) { btnSi.addEventListener('click', cerrar); }
  if (btnNo) { btnNo.addEventListener('click', cerrar); }
}

function conectarDetalle() {
  var btn = document.getElementById('btn-agregar-detalle');
  if (!btn) { return; }
  btn.addEventListener('click', function () {
    var id = new URLSearchParams(window.location.search).get('id');
    agregarAlCarrito(id);
  });
}

function pintarDetalle() {
  var contenedor = document.getElementById('detalle');
  if (!contenedor) { return; }
  var id = new URLSearchParams(window.location.search).get('id');
  var producto = null;
  for (var i = 0; i < PRODUCTOS.length; i++) {
    if (String(PRODUCTOS[i].id) === String(id)) { producto = PRODUCTOS[i]; break; }
  }
  if (!producto) {
    contenedor.innerHTML = '<div class="vacio">Producto no encontrado. <a href="index.html#catalogo">Volver al cat&aacute;logo</a></div>';
    return;
  }

  var img = document.createElement('img');
  img.className = 'detalle-img';
  img.src = producto.imagen;
  img.alt = producto.nombre;

  var info = document.createElement('div');
  var h1 = document.createElement('h1');
  h1.textContent = producto.nombre;
  info.appendChild(h1);

  var marca = document.createElement('p');
  marca.className = 'tarjeta-marca';
  marca.textContent = producto.marca.toUpperCase();
  info.appendChild(marca);

  var precio = document.createElement('div');
  precio.className = 'detalle-precio';
  precio.textContent = 'S/ ' + producto.precio.toFixed(2);
  info.appendChild(precio);

  var desc = document.createElement('p');
  desc.className = 'detalle-desc';
  desc.textContent = producto.descripcion;
  info.appendChild(desc);

  var ul = document.createElement('ul');
  ul.className = 'specs';
  for (var k in producto.specs) {
    if (!Object.prototype.hasOwnProperty.call(producto.specs, k)) { continue; }
    var li = document.createElement('li');
    var izq = document.createElement('span');
    izq.textContent = k;
    var der = document.createElement('span');
    der.textContent = producto.specs[k];
    li.appendChild(izq);
    li.appendChild(der);
    ul.appendChild(li);
  }
  info.appendChild(ul);

  var stock = document.createElement('p');
  stock.className = 'ayuda';
  stock.textContent = 'Stock disponible: ' + producto.stock + ' unidades';
  info.appendChild(stock);

  var btn = document.createElement('button');
  btn.className = 'btn btn-primario';
  btn.id = 'btn-agregar-detalle';
  btn.type = 'button';
  btn.textContent = 'Agregar al carrito';
  info.appendChild(btn);

  contenedor.innerHTML = '';
  contenedor.appendChild(img);
  contenedor.appendChild(info);
}

function iniciar() {
  leerCarrito();
  pintarOpcionesCategoria();
  pintarCatalogo();
  pintarCarrito();
  pintarDetalle();
  conectarCatalogo();
  conectarCarrito();
  conectarCheckout();
  conectarCuenta();
  conectarCookies();
  conectarDetalle();
  refrescarContador();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', iniciar);
} else {
  iniciar();
}
