<template>
  <mavon-editor
    ref="mavonEditor"
    :toolbars="toolbars"
    @imgAdd="$imgAdd"
    @change="change"
    @save="save"
    :boxShadow="false"
    v-model="markdown"
    :editable="editable"
    :subfield="subfield"
    :defaultOpen="defaultOpen"
  />
</template>

<script>
import Vue from 'vue'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import { uploadFile } from '@/api/index.js'
Vue.use(mavonEditor)
export default {
  name: 'Markdown',
  props: {
    value: {
      default: () => ({ markdown: '', html: '' })
    },
    editable: {
      type: Boolean,
      default: true
    },
    subfield: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      markdown: this.value.markdown,
      html: this.value.html,
      defaultOpen: this.editable ? null : 'preview',
      toolbars: {
        bold: this.editable, // 粗体
        italic: this.editable, // 斜体
        header: this.editable, // 标题
        underline: this.editable, // 下划线
        strikethrough: this.editable, // 中划线
        mark: this.editable, // 标记
        superscript: this.editable, // 上角标
        subscript: this.editable, // 下角标
        quote: this.editable, // 引用
        ol: this.editable, // 有序列表
        ul: this.editable, // 无序列表
        link: this.editable, // 链接
        imagelink: this.editable, // 图片链接
        code: this.editable, // code
        table: this.editable, // 表格
        fullscreen: true, // 全屏编辑
        readmodel: false, // 沉浸式阅读
        htmlcode: false, // 展示html源码
        help: true, // 帮助
        /* 1.3.5 */
        undo: this.editable, // 上一步
        redo: this.editable, // 下一步
        trash: this.editable, // 清空
        save: this.editable, // 保存（触发events中的save事件）
        /* 1.4.2 */
        navigation: this.editable, // 导航目录
        /* 2.1.8 */
        alignleft: this.editable, // 左对齐
        aligncenter: this.editable, // 居中
        alignright: this.editable, // 右对齐
        /* 2.2.1 */
        subfield: this.editable, // 单双栏模式
        preview: true // 预览
      }
    }
  },
  watch: {
    value () {
      this.markdown = this.value.markdown
      this.html = this.value.html
    }
  },
  methods: {
    async $imgAdd (filename, file) {
      const formdata = new FormData()
      formdata.append('file', file)
      const res = await uploadFile(formdata)
      if (res.code === 1) {
        const me = this.$refs.mavonEditor
        me.$img2Url(filename, res.data.url)
      } else {
        this.$Message.error('图片上传失败，请重试')
      }
    },
    /**
   * 清除掉 HTML 标签
   */
    wordCount (render) {
      let n = render.replace(/<\/?.+?\/?>/g, '')
      n = n.replace(/\s+/g, '')
      this.wordLength = n === '' ? 0 : n.length
    },
    change (value, render) {
      if (value === '' || render === '') {
        return
      }
      this.html = render
      this.wordCount(render)
      this.$emit('input', {
        markdown: value,
        html: render,
        contentLength: this.wordLength
      })
      this.$emit('change')
    },
    save () {
      this.$emit('save')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
