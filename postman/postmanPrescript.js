const CLOUD_CONVERSION_TOOL_BASE_API_URL = pm.environment.get('CLOUD_CONVERSION_TOOL_API_BASE_URL');
const username = pm.environment.get('DEFAULT_USERNAME');
const password = pm.environment.get('DEFAULT_PASSWORD');

const options = {
    url: `${CLOUD_CONVERSION_TOOL_BASE_API_URL}/api/auth/login`,
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            "username": username,
            "password": password
        })
    }
}

pm.sendRequest(options, function (error, response) {
    var jsonData = response.json();
    if (error) {
        console.log(error);
    }
    else {
        pm.environment.set('CLOUD_CONVERSION_TOOL_API_TOKEN', jsonData.accessToken)
    }
})