// Define os gatilhos de emoção
pub struct EmotionEngine {
    triggers: Vec<(String, Vec<String>, f32)>,
}

impl EmotionEngine {
    pub fn new() -> Self {
        EmotionEngine {
            triggers: vec![
                ("raiva".into(), vec!["idiota".into(), "burro".into()], 0.8),
                ("alegria".into(), vec!["amo".into(), "incrível".into()], 0.7),
            ],
        }
    }

    // Analisa texto e retorna emoção + intensidade
    pub fn analyze(&self, text: &str) -> (String, f32) {
        let text_lower = text.to_lowercase();
        for (emotion, words, intensity) in &self.triggers {
            if words.iter().any(|word| text_lower.contains(word)) {
                return (emotion.clone(), *intensity);
            }
        }
        ("neutro".into(), 0.1)
    }
}

// Exporta para C (usado via Python)
#[no_mangle]
pub extern "C" fn analyze_emotion(text: *const libc::c_char) -> *mut libc::c_char {
    let c_str = unsafe { std::ffi::CStr::from_ptr(text) };
    let text = c_str.to_str().unwrap();
    let engine = EmotionEngine::new();
    let (emotion, _) = engine.analyze(text);
    std::ffi::CString::new(emotion).unwrap().into_raw()
}
