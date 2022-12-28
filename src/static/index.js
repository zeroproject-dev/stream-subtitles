const $text = document.getElementById('text');

eel.expose(putText);
function putText(text) {
	text = JSON.parse(text);
	$text.textContent = text['partial'];
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
}

window.addEventListener('load', async () => {
	eel.start_voice_recognition();
	let settings = await eel.get_settings()();
	console.log(settings);
	setSettings(JSON.parse(settings));
});
