import '@h5web/app/dist/styles.css';
import React from 'react';
import { App, MockProvider } from '@h5web/app';
function MyApp() {
    return (React.createElement("div", { style: { height: '100vh' } },
        React.createElement(MockProvider, null,
            React.createElement(App, null))));
}
export default MyApp;
