import axios from 'axios';

const API_URL = 'https://localhost:5000';

// TODO get this actually hooked up
export async function getQuote(userId, stockSymbol, transNum) {
  // let endpoint = `/get/QUOTE/trans/${transNum}/user_id/${userId}/stock_symbol/${stockSymbol}`;
  // return await axios.get(`${API_URL}${endpoint}`)
  return 30.2;
}