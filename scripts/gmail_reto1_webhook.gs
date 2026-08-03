/**
 * Webhook Gmail — Misión Copilot 365 (Reto 1 / Reto 2)
 *
 * Por qué: PythonAnywhere gratuito suele bloquear SMTP (puerto 587).
 * Este script envía el correo con Gmail vía HTTPS.
 *
 * Setup (5 minutos):
 * 1. Entra a https://script.google.com con analizamostunegocio@gmail.com
 * 2. Nuevo proyecto → pega este código
 * 3. Edita WEBHOOK_SECRET (mismo valor que EMAIL_WEBHOOK_SECRET en .env de PA)
 * 4. Implementar → Nueva implementación → Tipo: Aplicación web
 *    - Ejecutar como: Yo
 *    - Quién tiene acceso: Cualquier persona
 * 5. Autoriza Gmail cuando Google lo pida
 * 6. Copia la URL que termina en /exec (NO uses /dev)
 * 7. En PythonAnywhere .env:
 *    EMAIL_WEBHOOK_URL=https://script.google.com/macros/s/XXXX/exec
 *    EMAIL_WEBHOOK_SECRET=el-mismo-secreto
 * 8. Web → Reload en PythonAnywhere
 *
 * Si cambias el código o el secreto: Implementar → Administrar implementaciones
 * → editar (lápiz) → Nueva versión → Implementar.
 */

const WEBHOOK_SECRET = "elige-un-secreto-largo"; // debe coincidir con EMAIL_WEBHOOK_SECRET

function doPost(e) {
  try {
    const data = JSON.parse((e && e.postData && e.postData.contents) || "{}");
    if (WEBHOOK_SECRET && data.secret !== WEBHOOK_SECRET) {
      return json_({ ok: false, error: "secret inválido" });
    }
    const to = String(data.to || "").trim();
    const subject = String(data.subject || "").trim();
    const body = String(data.body || "");
    const fromName = String(data.fromName || "Laura Méndez · Coordinación de Campo");
    if (!to || !subject || !body) {
      return json_({ ok: false, error: "faltan to/subject/body" });
    }
    GmailApp.sendEmail(to, subject, body, {
      name: fromName,
      replyTo: Session.getActiveUser().getEmail(),
    });
    return json_({ ok: true, to: to, subject: subject });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({
    ok: true,
    service: "Misión Copilot 365 · email webhook",
    hint: "POST JSON {to,subject,body,secret,fromName}",
  });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
