// Aplicar clases a forms de Django automáticamente
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input:not([type=radio]):not([type=checkbox]):not([type=submit]):not([type=file]):not(.otp-input):not(.form-control)').forEach(el => {
    el.classList.add('form-control');
  });
  document.querySelectorAll('select:not(.form-control)').forEach(el => el.classList.add('form-control'));
  document.querySelectorAll('textarea:not(.form-control)').forEach(el => el.classList.add('form-control'));

  // Auto-cerrar alertas después de 5 segundos
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });
});
