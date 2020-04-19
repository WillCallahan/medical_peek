module.exports = {
	"extends": [
		"eslint:recommended",
		"plugin:react/recommended"
	],
	"parser": "babel-eslint",
	"env": {
		"browser": true,
		"node": true,
		"jasmine": true,
		"es6": true
	},
	"rules": {
		"react/prop-types": 0,
		"semi": [2, "always"]
	},
	"settings": {
		"import/resolver": {
			"node": {
				"moduleDirectory": ["node_modules", "src/"]
			}
		}
	}
};