function cl(id) {
	flash('<img src="/img/ajax-loader.gif" alt="Loading..." />', true);
	$("#flash").load("/usr/form/" + id);
}
