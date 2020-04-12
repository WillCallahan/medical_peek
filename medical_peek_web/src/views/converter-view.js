import React, { useState } from 'react';
import withApiClient from "../hoc/with-api-client";
import { renderAlerts } from "../components/errors";

const ConverterView = (props) => {

	const [title, setTitle] = useState('');
	const [description, setDescription] = useState('');
	const [isLoading, setIsLoading] = useState(false);
	const [validations, setValidations] = useState([]);
	const [files, setFiles] = useState([]);
	const [errors, setErrors] = useState([]);

	const onTitleChange = (e) => {
		setTitle(e.target.value);
	};

	const onDescriptionChange = (e) => {
		setDescription(e.target.value);
	};

	const onFilesChange = (e) => {
		const rawFiles = e.target.files;
		let actualFiles = [];
		for (let i = 0; i < rawFiles.length; i++) {
			actualFiles.push(rawFiles[i]);
		}
		setFiles(actualFiles);
	};

	const getValidations = () => {
		let validations = [];
		if (!title) {
			validations.push('Title is required');
		}
		if (!files || !files.length) {
			validations.push('File is required');
		}
		return validations;
	};

	const getFileTitle = (file) => {
		if (file && file.current && file.current.title) {
			return ` - (${file.current.title})`;
		}
		return '';
	};

	const getFormData = () => {
		let formData = new FormData();

		for (let i = 0; i < files.length; i++) {
			formData.append(
				`file_content_${i}`,
				files[i],
				files[i].name
			);
		}

		formData.append(
			'title',
			title
		);

		formData.append(
			'description',
			description
		);

		return formData;
	};

	const uploadFile = (formData) => {
		return props.apiClient
			.post('/file-upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
			.then((r) => console.log('Uploaded file', r))
			.catch((e) => {
				setErrors(['Failed to process files']);
			});
	};

	const renderValidations = (validations) => {
		if (validations.length) {
			return (
				<div className="bd-callout bd-callout-warning">
					<h5>Please correct form errors</h5>
					<ul>
						{validations.map((v, i) => (<li key={`form-validation-${i}`} className={'text-danger font-weight-bold'}>{v}</li>))}
					</ul>
				</div>
			);
		}
		return (<></>);
	};

	const onSubmit = () => {
		const validations = getValidations();
		if (validations.length) {
			setValidations(validations);
		} else {
			setValidations([]);
			setIsLoading(true);
			const formData = getFormData();
			uploadFile(formData)
				.finally(() => setIsLoading(false));
		}
	};

	return (
		<>
			<h1 className="mt-5">Data Extractor</h1>
			<p className="lead">Extract data from images and PDFs into an Excel processable file.</p>
			<form>
				{renderValidations(validations)}
				{renderAlerts(errors)}
				<div className={"form-group"}>
					<label htmlFor={"file-title"}>Title</label>
					<input id={"file-title"} type={"text"} maxLength={"1024"} className={"form-control"} value={title} onChange={onTitleChange} disabled={isLoading} required={true}/>
				</div>
				<div className={"form-group"}>
					<label htmlFor={"file-description"}>Description</label>
					<textarea id={"file-description"} className={"form-control"} onChange={onDescriptionChange} value={description} disabled={isLoading}/>
					<small id="emailHelp" className="form-text text-muted">Aid in the identification of this
						document</small>
				</div>
				<div className="form-group">
					<label htmlFor="file-upload">File Upload {getFileTitle(files)}</label>
					<ul className="list-group mb-3">
						{files.map(f => (<li key={`li-file-${f.name}`} className="list-group-item">{f.name}</li>))}
					</ul>
					<input id="file-upload" type="file" className="form-control-file" disabled={isLoading} onChange={onFilesChange} multiple={true} accept={"image/jpeg,image/png,.pdf"} required={true}/>
				</div>
				<button type="button" className="btn btn-primary" onClick={onSubmit} disabled={isLoading}>
					{isLoading && <span className="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"/>}
					Submit
				</button>
			</form>
		</>
	);
};

export default withApiClient(ConverterView, 30000);