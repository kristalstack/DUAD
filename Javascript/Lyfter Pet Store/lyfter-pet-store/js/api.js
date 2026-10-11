// API layer: no DOM manipulation here.
const BASE='http://127.0.0.1:5000/api';
export const session=()=>JSON.parse(localStorage.getItem('lyfter_session')||'null');
export function saveSession(value){if(value)localStorage.setItem('lyfter_session',JSON.stringify(value));else localStorage.removeItem('lyfter_session')}
export async function request(path,{method='GET',body}={}){
 const headers={};if(body!==undefined)headers['Content-Type']='application/json';const token=session()?.access_token;if(token)headers.Authorization=`Bearer ${token}`;
 let response;try{response=await fetch(BASE+path,{method,headers,...(body!==undefined?{body:JSON.stringify(body)}:{})})}catch{throw Error('No se pudo conectar con el servidor. Comprueba que Flask esté funcionando.')}
 let data={};if(response.status!==204){try{data=await response.json()}catch{data={}}}
 if(!response.ok){if(response.status===401&&session()){saveSession(null);localStorage.removeItem('lyfter_cart')}throw Error(data.error||`Error HTTP ${response.status}`)}return data;
}
export const api={register:body=>request('/auth/register',{method:'POST',body}),login:body=>request('/auth/login',{method:'POST',body}),logout:()=>request('/auth/logout',{method:'POST'}),products:()=>request('/products'),product:id=>request(`/products/${id}`),createProduct:body=>request('/products',{method:'POST',body}),updateProduct:(id,body)=>request(`/products/${id}`,{method:'PATCH',body}),carts:()=>request('/carts'),newCart:()=>request('/carts',{method:'POST'}),cart:id=>request(`/carts/${id}`),setItem:(id,pid,quantity)=>request(`/carts/${id}/items/${pid}`,{method:'PUT',body:{quantity}}),removeItem:(id,pid)=>request(`/carts/${id}/items/${pid}`,{method:'DELETE'}),addresses:id=>request(`/users/${id}/addresses`),addAddress:(id,body)=>request(`/users/${id}/addresses`,{method:'POST',body}),checkout:(id,body)=>request(`/carts/${id}/checkout`,{method:'POST',body}),invoices:()=>request('/invoices')};
