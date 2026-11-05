/* =========================================================
   ElectroHogar · catálogo de productos (datos del sitio)
   ========================================================= */

var PRODUCTOS = [
  {
    id: 1,
    nombre: 'Audífonos Bluetooth SoulBeat X2',
    marca: 'SoulBeat',
    categoria: 'Audio',
    precio: 149.0,
    precioAntes: 199.0,
    stock: 12,
    destacado: true,
    etiquetas: ['audio', 'inalambrico', 'bluetooth', 'deporte'],
    imagen: 'assets/productos/audifonos.jpg',
    descripcion: 'Audífonos inalámbricos con cancelación activa de ruido, 32 horas de batería y estuche de carga USB-C.',
    specs: { 'Batería': '32 h', 'Conexión': 'Bluetooth 5.3', 'Peso': '48 g', 'Garantía': '12 meses' }
  },
  {
    id: 2,
    nombre: 'Licuadora PowerMix 1200',
    marca: 'PowerMix',
    categoria: 'Hogar',
    precio: 189.0,
    precioAntes: 249.0,
    stock: 8,
    destacado: true,
    etiquetas: ['hogar', 'cocina', 'electrodomestico'],
    imagen: 'assets/productos/licuadora.jpg',
    descripcion: 'Licuadora de vaso de vidrio de 1.5 L, 1200 W de potencia y 3 velocidades con función de licuado automático.',
    specs: { 'Potencia': '1200 W', 'Vaso': 'Vidrio 1.5 L', 'Velocidades': '3', 'Garantía': '12 meses' }
  },
  {
    id: 3,
    nombre: 'Laptop NovaBook 14',
    marca: 'Nova',
    categoria: 'Computadoras',
    precio: 2199.0,
    precioAntes: 2499.0,
    stock: 5,
    destacado: true,
    etiquetas: ['computo', 'portatil', 'oficina'],
    imagen: 'assets/productos/laptop.jpg',
    descripcion: 'Laptop de 14 pulgadas, procesador de 8 núcleos, 16 GB de memoria RAM y SSD de 512 GB.',
    specs: { 'Pantalla': '14" IPS', 'Memoria': '16 GB RAM', 'Disco': 'SSD 512 GB', 'Garantía': '24 meses' }
  },
  {
    id: 4,
    nombre: 'Smart TV Vision 43" 4K',
    marca: 'Vision',
    categoria: 'Televisores',
    precio: 1349.0,
    precioAntes: 1599.0,
    stock: 4,
    destacado: true,
    etiquetas: ['television', 'smarttv', 'video'],
    imagen: 'assets/productos/tv.jpg',
    descripcion: 'Televisor inteligente de 43 pulgadas con resolución 4K, aplicaciones integradas y control por voz.',
    specs: { 'Pantalla': '43" 4K', 'Audio': '20 W Dolby', 'Apps': 'Smart TV', 'Garantía': '12 meses' }
  },
  {
    id: 5,
    nombre: 'Cafetera Barista Mini',
    marca: 'Barista',
    categoria: 'Cocina',
    precio: 229.0,
    precioAntes: null,
    stock: 9,
    destacado: true,
    etiquetas: ['cocina', 'cafe', 'electrodomestico'],
    imagen: 'assets/productos/cafetera.jpg',
    descripcion: 'Cafetera compacta de 15 bares con vaporizador para leche,Depósito de 1.2 L y warming de tazas.',
    specs: { 'Presión': '15 bares', 'Depósito': '1.2 L', 'Vapor': 'Incluido', 'Garantía': '12 meses' }
  },
  {
    id: 6,
    nombre: 'Teclado Mecánico K-87',
    marca: 'KeyPro',
    categoria: 'Accesorios',
    precio: 259.0,
    precioAntes: 299.0,
    stock: 15,
    destacado: true,
    etiquetas: ['periferico', 'oficina', 'teclado'],
    imagen: 'assets/productos/teclado.jpg',
    descripcion: 'Teclado mecánico TKL de 87 teclas con switches redisables, retroiluminación y conexión multipunto.',
    specs: { 'Formato': 'TKL 87 teclas', 'Switches': 'Red switches', 'Conexión': 'BT + USB-C', 'Garantía': '12 meses' }
  },
  {
    id: 7,
    nombre: 'Tablet Tab S 11" 128 GB',
    marca: 'Tab',
    categoria: 'Tablets',
    precio: 899.0,
    precioAntes: 1049.0,
    stock: 7,
    destacado: true,
    etiquetas: ['tablet', 'movil', 'lectura'],
    imagen: 'assets/productos/tablet.jpg',
    descripcion: 'Tablet de 11 pulgadas con pantalla de 2K, 128 GB de almacenamiento y soporte para stylus.',
    specs: { 'Pantalla': '11" 2K', 'Almacenamiento': '128 GB', 'Peso': '480 g', 'Garantía': '12 meses' }
  },
  {
    id: 8,
    nombre: 'Smartwatch Fit Pulse 2',
    marca: 'Fit',
    categoria: 'Wearables',
    precio: 349.0,
    precioAntes: 429.0,
    stock: 11,
    destacado: true,
    etiquetas: ['reloj', 'deporte', 'salud'],
    imagen: 'assets/productos/smartwatch.jpg',
    descripcion: 'Smartwatch con GPS, monitor de ritmo cardíaco, AMOLED de 1.9" y 10 días de autonomía.',
    specs: { 'Pantalla': 'AMOLED 1.9"', 'Batería': '10 días', 'Sensores': 'GPS + FC', 'Garantía': '18 meses' }
  }
];

var CATEGORIAS = ['Audio', 'Hogar', 'Computadoras', 'Televisores', 'Cocina', 'Accesorios', 'Tablets', 'Wearables'];
