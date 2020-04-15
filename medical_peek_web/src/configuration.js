// eslint-disable-next-line no-unused-vars
const localConfiguration = {
	medicalPeekAddress: 'http://127.0.0.1:8000'
};

const devConfiguration = {
	medicalPeekAddress: 'http://127.0.0.1:8000'
};

const prodConfiguration = {
	medicalPeekAddress: 'https://medical-peek-api.callahanwilliam.com/v1'
};

const getConfiguration = () => {
	if (process.env.NODE_ENV === 'development') {
		return devConfiguration;
	} else {
		return prodConfiguration;
	}
};

export default getConfiguration;