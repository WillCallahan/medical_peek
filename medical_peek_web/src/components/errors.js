import React from 'react';

const renderAlerts = (errors) => {
	return errors.map((e, i) => (
		<div key={`alert-${i}`} className="alert alert-secondary" role="alert">
			{e}
		</div>
	));
};

export { renderAlerts };