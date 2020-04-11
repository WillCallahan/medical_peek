import React from 'react';
import axios from 'axios';
import { compose } from 'lodash/fp'
import withConfiguration from "./with-configuration";

const withApiClient = (WrappedComponent, timeout = 1000) => (props) => {
	const apiClient = axios.create({
		baseURL: props.configuration.medicalPeekAddress,
		timeout,
		headers: { 'X-Api-Client': 'React' }
	});
	const childProps = {
		...(props || {}),
		apiClient
	};
	return (<WrappedComponent {...childProps}/>)
};

export default compose(withConfiguration, withApiClient);