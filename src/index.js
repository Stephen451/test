import 'react-app-polyfill/stable';
import { render } from 'react-dom';
import './styles.css';
import MyApp from './MyApp';
const rootElement = document.getElementById('root');
render(React.createElement(MyApp, null), rootElement);
