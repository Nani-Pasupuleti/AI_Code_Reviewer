import React from 'react';

/**
 * Functional component that displays the login welcome screen.
 * 
 * @returns {JSX.Element} The rendered login screen component.
 */
const LoginScreen = () => {
    // Use const for variables that do not change
    const defaultUser = "admin";
    
    return (
        <div>
            <h1>Welcome {defaultUser}</h1>
        </div>
    );
};

export default LoginScreen;