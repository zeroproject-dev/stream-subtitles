const $text = document.getElementById('text');

eel.expose(putText);
function putText(text) {
	text = JSON.parse(text);
	split_text = text['partial'].split(' ');
	if (split_text.length === 1 && split_text[0] === '') {
		$text.innerHTML = '';
		return;
	}
	let $last = document.createElement('div');
	$text.innerHTML = split_text.join(' ');
	$text.appendChild($last);
	$last.scrollIntoView();
}

eel.expose(updateSettings);
function updateSettings(settings) {
	settings = JSON.parse(settings);
	setSettings(settings);
}

function setSettings(settings) {
	let { style } = document.documentElement;
	style.setProperty('--font-size', settings['font_size'] + 'pt');
	style.setProperty('--font-color', settings['color']);
	style.setProperty('--opacity', settings['background_opacity']);
	style.setProperty('--font-family', settings['font_family']);
}

window.addEventListener('load', async () => {
	eel.start_voice_recognition();
	let settings = await eel.get_settings()();
	setSettings(JSON.parse(settings));
});
