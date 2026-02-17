import { useEffect } from "react";
import axios from "axios";

function App() {
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/health")

      .then(res => console.log(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>🎓 Online Exam Proctoring System</h1>
      <p>Frontend Connected to Backend 🚀</p>
    </div>
  );
}

export default App;
