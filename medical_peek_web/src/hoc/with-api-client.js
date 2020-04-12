import React from 'react';
import axios from 'axios';
import _ from 'lodash';
import { compose } from 'lodash/fp';
import withConfiguration from "./with-configuration";

const withApiClient = (WrappedComponent, timeout = 1000) => (props) => {

	const apiClient = axios.create({
		baseURL: props.configuration.medicalPeekAddress,
		timeout,
		headers: { 'X-Api-Client': 'React' },
	});

	apiClient.interceptors.response.use((response) => {
		if (_.has(response, 'data')) {
			return response.data;
		} else {
			console.warn('Unable to get the response data', response);
			return response;
		}
	});

	const childProps = {
		...(props || {}),
		apiClient
	};

	return (<WrappedComponent {...childProps}/>);
};

export default compose(withConfiguration, withApiClient);