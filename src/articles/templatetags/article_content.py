import re

from django import template
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.filter
def format_article_content(content):
    normalized_content = content.replace('\r\n', '\n').replace('\r', '\n')
    blocks = (block.strip() for block in normalized_content.split('\n\n'))
    rendered_blocks = []

    for block in blocks:
        if not block:
            continue

        if block.startswith('### '):
            rendered_blocks.append(format_html('<h3>{}</h3>', block[4:]))
        elif block.startswith('## '):
            rendered_blocks.append(format_html('<h2>{}</h2>', block[3:]))
        else:
            lines = format_html_join(
                '<br>',
                '{}',
                ((line.strip(),) for line in block.splitlines()),
            )
            rendered_blocks.append(format_html('<p>{}</p>', lines))

    return format_html_join('\n', '{}', ((block,) for block in rendered_blocks))


@register.simple_tag
def render_article_body(article):
    normalized_content = article.content.replace('\r\n', '\n').replace('\r', '\n')
    blocks = (block.strip() for block in normalized_content.split('\n\n'))
    images = {image.marker: image for image in article.inline_images.all()}
    rendered_blocks = []

    for block in blocks:
        if not block:
            continue

        match = re.fullmatch(r'\[\[imagen:([a-zA-Z0-9_-]+)\]\]', block)
        if match:
            image = images.get(match.group(1))
            if image:
                if image.caption:
                    if image.image:
                        image_element = format_html(
                            '<img src="{}" alt="{}" loading="lazy" decoding="async">',
                            image.image.url,
                            image.alt_text,
                        )
                    else:
                        image_element = format_html(
                            '<img src="{}" alt="{}" loading="lazy" decoding="async">',
                            static(f'articles/images/{image.illustration}.svg'),
                            image.alt_text,
                        )
                    rendered_blocks.append(format_html(
                        '<figure class="article-figure">{}<figcaption>{}</figcaption></figure>',
                        image_element,
                        image.caption,
                    ))
                else:
                    if image.image:
                        image_element = format_html(
                            '<img src="{}" alt="{}" loading="lazy" decoding="async">',
                            image.image.url,
                            image.alt_text,
                        )
                    else:
                        image_element = format_html(
                            '<img src="{}" alt="{}" loading="lazy" decoding="async">',
                            static(f'articles/images/{image.illustration}.svg'),
                            image.alt_text,
                        )
                    rendered_blocks.append(format_html(
                        '<figure class="article-figure">{}</figure>',
                        image_element,
                    ))
            else:
                rendered_blocks.append(format_html('<p>{}</p>', block))
        elif block.startswith('### '):
            rendered_blocks.append(format_html('<h3>{}</h3>', block[4:]))
        elif block.startswith('## '):
            rendered_blocks.append(format_html('<h2>{}</h2>', block[3:]))
        else:
            lines = format_html_join(
                '<br>',
                '{}',
                ((line.strip(),) for line in block.splitlines()),
            )
            rendered_blocks.append(format_html('<p>{}</p>', lines))

    return format_html_join('\n', '{}', ((block,) for block in rendered_blocks))
