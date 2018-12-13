import React from 'react';
import {
  BarChart,
  CartesianGrid,
  YAxis,
  XAxis,
  Tooltip,
  Bar,
  Label,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { Container, Header } from 'semantic-ui-react';
import { interpolateRdPu } from 'd3-scale-chromatic';

import { profilesMapping } from '../modelView/reportMapping';

const data = [
  { profileName: 'AAD', count: 16 },
  { profileName: 'AP', count: 46 },
  { profileName: 'APO', count: 19 },
  { profileName: 'ART_A', count: 68 },
  { profileName: 'ART_D', count: 31 },
  { profileName: 'CAP', count: 35 },
  { profileName: 'CCE', count: 45 },
  { profileName: 'CCO', count: 49 },
  { profileName: 'CON', count: 24 },
  { profileName: 'ED', count: 35 },
  { profileName: 'EM', count: 34 },
  { profileName: 'EMP', count: 26 },
  { profileName: 'EP', count: 29 },
  { profileName: 'EPF', count: 15 },
  { profileName: 'I', count: 42 },
  { profileName: 'IC', count: 43 },
  { profileName: 'ICOOP', count: 53 },
  { profileName: 'IJ', count: 42 },
  { profileName: 'IS', count: 35 },
  { profileName: 'IV', count: 28 },
  { profileName: 'IVD', count: 43 },
  { profileName: 'IVE', count: 30 },
  { profileName: 'IVM', count: 23 },
  { profileName: 'IVP', count: 36 },
  { profileName: 'JI', count: 23 },
  { profileName: 'LIB', count: 24 },
  { profileName: 'MR', count: 4 },
  { profileName: 'PAT', count: 22 },
  { profileName: 'PCI', count: 23 },
  { profileName: 'PERS', count: 32 },
  { profileName: 'PF', count: 21 },
  { profileName: 'PID', count: 54 },
  { profileName: 'RNL', count: 17 },
  { profileName: 'TD', count: 34 },
  { profileName: 'TEC', count: 22 },
  { profileName: 'TG', count: 44 },
  { profileName: 'TM', count: 43 },
  { profileName: 'VV', count: 10 }
];
const margin = { top: 5, right: 5, bottom: 50, left: 5 };
function GlobalReportChart(props) {
  const sortedData = data.sort((a, b) => b.count - a.count);
  return (
    <Container style={{ height: '100vh' }}>
      <Header style={{ fontSize: '2.5em' }}>
        Análisis global de los perfiles
      </Header>
      <div style={{ height: '50%' }}>
        <ResponsiveContainer ratio={2.4} width="100%">
          <BarChart data={sortedData} margin={margin} barCategoryGap="20%">
            <defs>
              <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#b92b27" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#1565C0" stopOpacity={0.8} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="profileName"
              type="category"
              interval={0}
              tick={{ angle: -35, textAnchor: 'end' }}
            >
              <Label
                value="Nombre del perfil"
                offset={-30}
                position="insideBottom"
              />
            </XAxis>
            <YAxis>
              <Label
                value="Conteo de grupos"
                angle={-90}
                position="insideLeft"
              />
            </YAxis>
            <Tooltip labelFormatter={label => profilesMapping[label]} />
            <Bar
              dataKey="count"
              name="Cantidad de grupos"
              fill="url(#colorCount)"
              animationDuration={1500}
              animationEasing="ease-out"
              barSize={20}
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={interpolateRdPu(entry.count / 38)}
                  strokeWidth={4}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <Container textAlign="justified" style={{ marginTop: '5%' }}>
        <p>
          En la gráfica anterior se observa la cantidad de veces en la que los
          grupos de la Universidad Tecnológica estuvieron por debajo en la
          medida de cada perfil con respecto a su grupo más cercano en la
          clasificación superior a la suya.
        </p>
        <p>
          Se aprecia que los Artículos de investigación (ART_A) del perfil de
          productos resultado de actividades de generación de nuevo conocimiento
          es la componente más débil seguida por los proyectos investigación y
          desarrollo (PID) del perfil de productos resultado de actividades
          relacionadas con la formación del recurso humano en CTI.
        </p>
        <p>
          En tercer lugar está el indicador de cooperación (ICOOP) que busca
          evidenciar el trabajo en conjunto entre los grupos de investigación a
          partir de la coautorías. En cuarto lugar la componente del perfil de
          productos resultado de actividades de apropiación social del
          conocimiento, comunicación social del conocimiento (CCO) y en quinto
          lugar, apoyo a programas de formación (AP), componente del perfil de
          productos resultado de actividades relacionadas con la formación del
          recurso humano en CTI.
        </p>
      </Container>
    </Container>
  );
}

export default GlobalReportChart;
