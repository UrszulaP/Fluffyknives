ClassicEditor
  .create(document.querySelector('#editor'), {
    removePlugins: ['Heading', 'BlockQuote'],
    toolbar: ['bold', 'italic', 'link', 'bulletedList', 'numberedList'],
  })
  .catch(error => {
    console.log(error);
  });
