import './App.css';
import Header from './components/Header/Header';
import Main from './components/Main/Main';
import { BrowserRouter as Router} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Header />
      <Main />
    </Router>
  );
}

export default App;
