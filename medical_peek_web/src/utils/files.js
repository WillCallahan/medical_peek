const saveAsCsv = (fileName, data) => {
	const fileContents = data.map(r => r.join(',')).join('\n');
	const fileContentsWithType = `data:text/csv;charset=utf-8,${fileContents}`;
	const windowContents = encodeURI(fileContentsWithType);
	const link = document.createElement('a');
	link.setAttribute('href', windowContents);
	link.setAttribute('download', fileName);
	document.body.appendChild(link);
	link.click();
	window.open(fileName);
	document.removeChild(link);
};

const buildFileName = (fileName) => {
	return fileName.toString().replace(/ /g, '_').replace(/[^\w_\s]/g, '');
};

export { saveAsCsv, buildFileName };