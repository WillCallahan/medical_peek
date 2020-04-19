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
		console.debug('Pulling response data from response', response);
		if (_.has(response, 'data')) {
			console.debug('Response has data property; returning data', response.data);
			return response.data;
		} else {
			console.warn('Unable to get the response data', response);
			return response;
		}
	}, error => {
		console.error('An error occurred during the processing of an AJAX request', error);
		return Promise.reject(error);
	});

	const childProps = {
		...(props || {}),
		apiClient
	};

	return (<WrappedComponent {...childProps}/>);
};

export default compose(withConfiguration, withApiClient);