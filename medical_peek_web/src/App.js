import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min'
import React from 'react';
import './App.css';
import mainContent from './components/content'
import headContent from './components/head'
import footContent from './components/foot'
import converterView from './views/converter-view'

const App = () => {
	return (
		<>
			{headContent()}
			{mainContent({content: converterView()})}
			{footContent()}
		</>
	);
};

export default App;
