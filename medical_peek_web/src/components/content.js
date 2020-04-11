import React from 'react';

const mainContent = (props) => {
	return (
		<main role="main" className="container main-content">{props.content}</main>
	);
};

export default mainContent;