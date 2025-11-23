// Simulating a Junior Developer's React code
import React from 'react';

const login_screen = () => { // Error: Component should be PascalCase (LoginScreen)
    var user = "admin"; // Error: Use 'const' or 'let', never 'var'
    
    console.log("User logging in..."); // Error: No console logs in production
    
    return (
        <div>
            <h1>Welcome {user}</h1>
        </div>
    );
};

export default login_screen;
