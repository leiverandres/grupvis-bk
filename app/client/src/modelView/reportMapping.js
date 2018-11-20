export const profilesMapping = {
  IS: 'investigador sénior',
  I: 'investigador asociado',
  IJ: 'investigador junior',
  ED: 'estudiante de doctorado',
  EM: 'estudiante de maestría o especialidad clínica',
  JI: 'joven investigador',
  EP: 'estudiante de pregrado',
  IVD: 'integrante vinculado con doctorado',
  IVM: 'integrante vinculado con maestría o especialidad clínica',
  IVP: 'integrante vinculado con pregrado',
  IVE: 'integrante vinculado con especialización',
  IV: 'integrante vinculado',
  IC: 'indicador de cohesión',
  ICOOP: 'indicador de colaboración',
  ART_A: 'artículos de investigación A1, A, B y C',
  ART_D: 'artículos de investigación D',
  LIB: 'libros de investigación',
  CAP: 'capítulos de investigación',
  PAT: 'productos tecnológicos patentados',
  VV: 'variedades vegetales y animales',
  AAD: 'Obras de arte, arquitectura o diseño',
  TEC: 'productos tecnológicos certificados o validados',
  EMP: 'productos empresariales',
  RNL: 'regulaciones, normas y reglamentos técnicos',
  CON: 'consultorías científicas y tecnológicas',
  MR:
    'registros de acuerdos de licencia para la explotación de obras de AAD (Arte, Arquitectura o Diseño)e protegidad por derecho de autor',
  PCI: 'participación ciudadana en CTI',
  EPF: 'estrategias pedagógicas para el fomento de la CTI',
  CCO: 'comunicación social del conocimiento',
  CCE: 'circulación de conocimiento especializado',
  TD: 'tesis de doctorado',
  TM: 'trabajo de grado de maestría',
  TG: 'trabajo de grado de pregrado',
  PID: 'proyectos de investigación y desarrollo',
  PF: 'proyectos de investigación, desarrollo e innovación (ID+I)',
  PERS: 'proyectos de extensión y responsabilidad social en CTI',
  AP: 'apoyo a programas de formación',
  APO: 'acompañamientos y asesorías de linea temática del Programa Ondas'
};

export const productSubtypes = {
  IC: [
    'Valor que permite evidenciar la colaboración (coautorías) a nivel interno de los integrantes del Grupo de Investigación, Desarrollo Tecnológico o Innovación.'
  ],
  ICOOP: [
    'Valor con el que se busca evidenciar el trabajo conjunto (coautoría) entre grupos. '
  ],
  LIB: ['Libros A1', 'Libros A', 'Libros B'],
  CAP: ['Capítulo de Libro A1', 'Capítulo de Libro A', 'Capítulo de Libro B'],
  PAT: [
    'Patente de Invención A1',
    'Patente de Invención A2',
    'Patente de Invención A3',
    'Patente de Invención A4',
    'Patente de Invención B1',
    'Patente de Invención B2',
    'Patente de Invención B3',
    'Patente de Invención B4',
    'Patente de Invención B5',
    'Patente de Invención C'
  ],
  VV: [
    'Variedad Vegetal A1',
    'Variedad Vegetal A2',
    'Variedad Vegetal A3',
    'Variedad Vegetal A4',
    'Variedad Vegetal B1',
    'Variedad Vegetal B2',
    'Variedad Vegetal B3',
    'Variedad Vegetal B4',
    'Variedad Animal A'
  ],
  AAD: [
    'Obras Artes Arquitectura Diseño A1',
    'Obras Artes Arquitectura Diseño A',
    'Obras Artes Arquitectura Diseño B',
    'Obras Artes Arquitectura Diseño C'
  ],
  TEC: [
    'Diseño industrial',
    'Esquema de circuito integrado',
    'Software',
    'Planta piloto',
    'Prototipo industrial',
    'Signos distintivos'
  ],
  EMP: [
    'Secreto empresarial',
    'Empresa de base tecnológica',
    'Empresas Creativas y Culturales',
    'Innovación Generada en la Gestión Empresarial',
    'Innovación en procedimiento y servicio'
  ],
  RNL: [
    'Regulaciones, normas, reglamentos o legislaciones',
    'Guía de Práctica Clínica (GPC)',
    'Proyecto de Ley'
  ],
  CON: [
    'Consultoría científicas-tecnologías',
    'Consultoría de procesos en investigación-creación en arte, arquitectura y diseño',
    'Informe técnico final'
  ],
  TD: ['Tesis de Doctorado laureada o meritoria', 'Tesis de Doctorado'],
  TM: [
    'Trabajo de grado de maestría laureado o meritorio',
    'Trabajo de grado de maestría'
  ],
  TG: [
    'Trabajo de grado de pregrado con distinción',
    'Trabajo de grado de pregrado'
  ],
  PID: [
    'Proyecto de Investigación y Desarrollo (Financiación externa Internacional)',
    'Proyecto de Investigación y Desarrollo (Financiación externa nacional)',
    'Proyecto de Investigación y Desarrollo (Financiación interna)'
  ],
  PF: [
    'Proyecto ID+I con formación (Con investigadores)',
    'Proyecto ID+I con formación (Con jovenes invetigadores)'
  ],
  AP: [
    'Programas de doctorado',
    'Programas de maestría',
    'Cursos de doctorado',
    'Cursos de maestría'
  ]
};

export const membersProfile = [
  'IS',
  'I',
  'IJ',
  'ED',
  'EM',
  'JI',
  'EP',
  'IVD',
  'IVM',
  'IVP',
  'IVE',
  'IV'
];

export const colaborationProfile = ['IC', 'ICOOP'];

export const newKnowledgeProductionProfile = [
  'ART_A',
  'ART_D',
  'LIB',
  'CAP',
  'PAT',
  'VV',
  'AAD'
];

export const technologicalDevelopmentProfile = [
  'TEC',
  'EMP',
  'RNL',
  'CON',
  'MR'
];

export const socialAppropriationProfile = ['PCI', 'EPF', 'CCO', 'CCE'];

export const humanResourceFormationProfile = [
  'TD',
  'TM',
  'TG',
  'PID',
  'PF',
  'PERS',
  'AP',
  'APO'
];
