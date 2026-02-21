// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://localhost:8000",
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// export default api;


import axios from "axios";

// This tells the app: "Use the live Render URL, but if that's missing, use localhost."
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://todosapp-fwas.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
