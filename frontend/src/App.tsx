import './App.css'

function App() {

  const sendBudget = async (formData: FormData) => {

    const budget = formData.get("budget"); 
    alert(budget)

    const budgetInfo: RequestInit = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ budgetInfo: budget })
    };
  await fetch('http://127.0.0.1:5000/submitSiteData', budgetInfo)
      .then(response => response.json())
      .then(data => console.log('Success:', data))
      .catch(error => console.error('Error:', error));
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
      
        </div>

        
      </section>

    </>
  )
}

export default App
