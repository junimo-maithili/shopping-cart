import './App.css'
import Login from './assets/Login';
import { useState } from "react";

function App() {

  const [uuid, setUuid] = useState<string | null>(null);

  const sendBudget = async (formData: FormData) => {
    console.log("CALLED SEND BUDGET")

    const budget = formData.get("budget");

    const newUuid = await getExtensionUUID();
    setUuid(newUuid)

  
    const budgetInfo: RequestInit = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ budgetInfo: budget, uuid: newUuid })
    };
    console.log("fetching now!")

    await fetch('http://127.0.0.1:5000/submitSiteData', budgetInfo)
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));

      
  }

  function getExtensionUUID() {
    return new Promise<string | null>((resolve) => {  
      const handler = (event: MessageEvent) => {
        console.log("Received message:", event.data);

  
        if (event.data.type !== "RETURN_UUID") {
          return;
        }
  
        window.removeEventListener("message", handler);
        resolve(event.data.uuid);
      };
  
      window.addEventListener("message", handler);
  
      console.log("Website requesting UUID");
  
      window.postMessage(
        {
          type: "GET_UUID"
        },
        "*"
      );
    });
  }



  return (
    <>
        <div>
          <Login uuid={uuid}/>
        </div>
       
      <section id="center">
        <div>
          <h1>Shopping Cart</h1>
          <div>
            <p>Set a budget you'd like to follow!</p>
            <p>Shopping Cart will send you messages top encourage you not to spend too much on Amazon.</p>
            <form action={sendBudget}>
            <br/><br/><br/>
              <label>
                Budget <br/>
                <input type="text" name="budget" />
              </label>
              <input type="submit" value="Submit"/>
            </form>
          </div>

          <div>
            <br/><br/><br/>
          
            

          </div>
      
        </div>

        
      </section>

    </>
  )
}

export default App