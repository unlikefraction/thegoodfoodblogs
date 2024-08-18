document.addEventListener("DOMContentLoaded", function() {
    // Select all <a> tags inside elements with the class "blog"
    const links = document.querySelectorAll('.blog a');

    // Function to check if a URL is external
    function isExternal(url) {
        const domain = (new URL(url)).hostname;
        return domain !== window.location.hostname;
    }

    // Iterate over each <a> tag
    links.forEach(link => {
        if (isExternal(link.href)) {
            // Add target="_blank" to external links
            link.setAttribute('target', '_blank');
            // Append 🔗 to the end of the link text
            link.innerHTML += ' 🔗';
        }
    });

    // Select the blog content to search for paired parentheses
    const blogContent = document.querySelector('.blog_content');

    // Function to wrap paired parentheses in a span with the class "faded"
    function wrapParentheses(content) {
        return content.replace(/\(([^)]+)\)/g, '<span class="faded">($1)</span>');
    }

    // If blogContent exists, wrap the paired parentheses
    if (blogContent) {
        blogContent.innerHTML = wrapParentheses(blogContent.innerHTML);
    }
});
