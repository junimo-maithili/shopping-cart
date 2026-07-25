import './App.css'
import Login from './assets/Login';
import { useState } from "react";

function App() {

  const [uuid, setUuid] = useState<string | null>(null);

  const sendBudget = async (formData: FormData) => {
    console.log("CALLED SEND BUDGET")

    const budget = formData.get("budget");
    alert(budget)
    const newUuid = await getExtensionUUID();
    setUuid(newUuid)
    console.log("SET UUID")

  
    const budgetInfo: RequestInit = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ budgetInfo: budget, uuid: newUuid })
    };

    await fetch('http://127.0.0.1:5000/submitSiteData', budgetInfo)
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
  }

  function getExtensionUUID() {
    return new Promise<string | null>((resolve) => {
  
      const handler = (event: MessageEvent) => {
  
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
      <section id="center">
       
        <div>
          <h1>Set Budget</h1>
          <p>Turn this into a react component</p>
          <div>
            <h2>category</h2>
            <p>set price</p>
            <form action={sendBudget}>
              <label>
                category <br/>
                <input type="text" name="budget" />
              </label>
              <input type="submit" value="Submit"/>
            </form>
          </div>

          <div>
            <br/><br/><br/>
            <Login uuid={uuid}/>
            

          </div>
      
        </div>

        
      </section>

    </>
  )
}

export default App