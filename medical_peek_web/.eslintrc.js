module.exports = {
	"extends": [
		"eslint:recommended",
		"plugin:react/recommended"
	],
	"parser": "babel-eslint",
	"env": {
		"browser": true,
		"node": true,
		"jasmine": true
	},
	"rules": {
		"react/prop-types": 0
	},
	"settings": {
		"import/resolver": {
			"node": {
				"moduleDirectory": ["node_modules", "src/"]
			}
		}
	}
};