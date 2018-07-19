import toastr from '../../assets/js/toastr.min.js'
export default function(type, title, msg) {
	if(type == "success"){
		toastr.success(msg,title);
	}
	else if(type == "info") {
		toastr.info(msg, title);
	}
	else if(type == "error"){
		toastr.error(msg,title);
	}
	else {
		toastr.warning(msg, title);
	}
}