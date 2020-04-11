import React from 'react';
import getConfiguration from '../configuration';

const withConfiguration = (WrappedComponent) => (props) => {
	const configuration = getConfiguration();
	const childProps = {
		...(props || {}),
		configuration
	};
	return (<WrappedComponent {...childProps} />);
};

export default withConfiguration;
