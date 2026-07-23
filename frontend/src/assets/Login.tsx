import { loginWithGoogle } from "../auth"

const Login = () => {

  async function login () {

    const uuid = await loginWithGoogle()

    // Send UUID to backend
    const fbId: RequestInit = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uuid })
      };
    await fetch('http://127.0.0.1:5000/submitFbId', fbId)
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    }


  return (

    <div>
        <button onClick={login}>Login</button>
                  
    </div>
  )
}

export default Login
