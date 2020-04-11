import React from 'react';
import axios from 'axios';

const withApiClient = (WrappedComponent) => (props) => {
	const apiClient = axios.create({
		baseURL: 'https://medical-peek.callahanwilliam.com/dev/',
		timeout: 1000,
		headers: {'X-Api-Client': 'React'}
	});
	return (<WrappedComponent props={{...props, apiClient}}/>)
};

export default withApiClient;