/**
 * Webhook Gmail para Reto 1 — Misión Copilot 365
 *
 * Por qué: PythonAnywhere gratuito suele bloquear SMTP (puerto 587).
 * Este script envía el correo con Gmail vía HTTPS.
 *
 * Setup (5 minutos):
 * 1. Entra a https://script.google.com con analizamostunegocio@gmail.com
 * 2. Nuevo proyecto → pega este código
 * 3. Implementar → Nueva implementación → Tipo: Aplicación web
 *    - Ejecutar como: Yo
 *    - Quién tiene acceso: Cualquier persona
 * 4. Copia la URL de la implementación
 * 5. En PythonAnywhere .env agrega:
 *    EMAIL_WEBHOOK_URL=https://script.google.com/macros/s/XXXX/exec
 *    EMAIL_WEBHOOK_SECRET=elige-un-secreto-largo
 * 6. Pon el MISMO secreto abajo en WEBHOOK_SECRET
 * 7. Web → Reload en PythonAnywhere
 */

const WEBHOOK_SECRET = "elige-un-secreto-largo"; // debe coincidir con EMAIL_WEBHOOK_SECRET

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents || "{}");
    if (WEBHOOK_SECRET && data.secret !== WEBHOOK_SECRET) {
      return json_({ ok: false, error: "secret inválido" });
    }
    const to = (data.to || "").trim();
    const subject = (data.subject || "").trim();
    const body = data.body || "";
    const fromName = data.fromName || "Laura Méndez · Coordinación de Campo";
    if (!to || !subject || !body) {
      return json_({ ok: false, error: "faltan to/subject/body" });
    }
    GmailApp.sendEmail(to, subject, body, {
      name: fromName,
      replyTo: Session.getActiveUser().getEmail(),
    });
    return json_({ ok: true, to: to });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, service: "Misión Copilot 365 · Reto 1 webhook" });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
