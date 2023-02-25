function inject_css(css_code) {
  const style = document.createElement('style');
  style.textContent = css_code;
  document.head.appendChild(style);
}

function set_background_color(color) {
  console.info('Setting background color to', color);

  inject_css(`
        body {
            background-color: ${color};
        }
    `);
}

/** @param {{src, position, repeat, size}} image */
function set_background_image(image) {
  console.info('Setting background image to', image);

  inject_css(`
        body {
            background-image: url('${image.src}');
            background-position: ${image.position};
            background-repeat: ${image.repeat};
            background-size: ${image.size};
        }
    `);
}

function set_background_video(video_url) {
  console.info('Setting background video to', video_url);

  const video_node = document.createElement('video');
  video_node.src = video_url;
  video_node.id = 'background-video';
  video_node.autoplay = true;
  video_node.loop = true;
  video_node.muted = true;

  document.body.appendChild(video_node);
  inject_css(`
        #background-video {
            position: fixed;
            top: 0;
            height: 100vh;
            width: 100vw;
            z-index: -1;
        }

        body {
            background-color: #000;
        }
    `);
}

export default {
  mounted() {
    if (!this.$props) return;

    const prop_type = Object.keys(this.$props)[0];

    switch (prop_type) {
      case 'color':
        set_background_color(this.$props.color);
        break;

      case 'image':
        set_background_image(this.$props.image);
        break;

      case 'video':
        set_background_video(this.$props.video);
        break;

      default:
        break;
    }
  },
  props: {
    color: String,
    image: Object,
    video: String,
  },
};
