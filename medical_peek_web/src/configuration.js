// eslint-disable-next-line no-unused-vars
const localConfiguration = {
	medicalPeekAddress: 'http://127.0.0.1:8000'
};

const devConfiguration = {
	medicalPeekAddress: process.env.MEDICAL_PEEK_API_URL || 'http://127.0.0.1:8000'
};

const prodConfiguration = {
	medicalPeekAddress: process.env.MEDICAL_PEEK_API_URL || 'https://medical-peek-api.callahanwilliam.com'
};

const getConfiguration = () => {
	if (process.env.NODE_ENV === 'development') {
		return devConfiguration;
	} else {
		return prodConfiguration;
	}
};

export default getConfiguration;