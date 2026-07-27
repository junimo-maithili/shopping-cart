import { loginWithGoogle } from "../auth"

interface LoginProps {
  uuid: string | null;
}

function Login({ uuid }: LoginProps) {


  async function login () {

    const firebaseUuid = await loginWithGoogle()

    console.log("Firebase UUID:", firebaseUuid);
    console.log("Extension UUID:", uuid);


    // Send UUID to backend
    const fbId: RequestInit = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ firebaseUuid, uuid })
      };
    await fetch('http://127.0.0.1:5000/submitFbId', fbId)
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    }


  return (

    <div id="login-bar">
        <button onClick={login}>Login</button>
                  
    </div>
  )
}

export default Login
