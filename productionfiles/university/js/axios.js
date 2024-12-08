import { getCSRFToken } from "./getCsrfToken.js";

axios.defaults.headers.common["X-CSRFToken"] = getCSRFToken();

let axiosHeader = axios;
export default axiosHeader;
