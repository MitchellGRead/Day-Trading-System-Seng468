import axios from 'axios';

const API_URL = 'https://localhost:5000';

// TODO get this actually hooked up
export async function getQuote(userId, stockSymbol, transNum) {
  let endpoint = `/get/QUOTE/trans/${transNum}/user_id/${userId}/stock_symbol/${stockSymbol}`;
  return await axios.get(`${API_URL}${endpoint}`)
}

export async function postFunds(userId, funds) {
  let endpoint = `/add`;
  let data = {
    'user_id': userId,
    'amount': funds,
    'command': 'ADD',
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}