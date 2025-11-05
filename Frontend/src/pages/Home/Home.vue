<template>
  <div class="home-page">
    <h2 class="page-title">Home - <span class="fw-semi-bold">OpenAPI</span></h2>
    <b-row>
      <div class="pb-xlg h-100">
        <Widget
          title="<h5>Selamat Datang Developer <small class='text-muted'> POS OpenAPI Site</small></h5>"
          customHeader close collapse
        >
          <p style="line-height: 1.2;"><strong>UPDATE : Dokumen Standar Versi 1.0.1 (November 2021)</strong></p>
          <p style="text-align: justify;">SNAP&nbsp;<em>Developer Site</em>&nbsp;hadir untuk mendukung implementasi Standar Nasional&nbsp;<em>Open</em>&nbsp;API Pembayaran (SNAP).</p>
          <p style="text-align: justify;">SNAP&nbsp;<em>Developer Site</em>&nbsp;merupakan media bagi para&nbsp;<em>developer</em>&nbsp;yang mengembangkan&nbsp;<em>Open</em>&nbsp;API Pembayaran untuk mempelajari spesifikasi API pembayaran yang distandarkan oleh Standar Nasional&nbsp;<em>Open</em>&nbsp;API Pembayaran (SNAP).</p>
          <p style="text-align: justify;">SNAP&nbsp;<em>Developer Site</em>&nbsp;juga merupakan media bagi&nbsp;<em>developer</em>&nbsp;untuk melakukan pengujian API pembayaran pada aplikasi pengujian&nbsp;<em>Open</em>&nbsp;API Pembayaran berbasis SNAP.</p>
          <p style="text-align: justify;">Selain itu, SNAP&nbsp;<em>Developer Site</em>&nbsp;juga menyediakan Direktori Publikasi yang akan mempublikasikan para pihak yang telah memiliki&nbsp;<em>Open</em>&nbsp;API Pembayaran berbasis SNAP yang telah terverifikasi.</p>
          <p style="text-align: justify;"><strong>Apa fungsi SNAP Developer Site?</strong></p>
          <p style="text-align: justify;">Fungsi SNAP Developer Site adalah:</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Publikasi standar teknis dan keamanan, standar data, dan spesifikasi teknis berbasis SNAP</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Aplikasi pengujian Open API Pembayaran berbasis SNAP</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Direktori Publikasi pihak yang telah menerapkan standar teknis dan keamanan, standar data, dan spesifikasi teknis berbasis SNAP</p>
          <p style="text-align: justify;"><strong>Bagaimana mengakes standar teknis dan keamanan, standar data, dan spesifikasi teknis berbasis SNAP?</strong></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Pilih menu “API” untuk melihat daftar API yang distandarkan oleh SNAP.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Pada halaman yang dipilih akan berisi dokumentasi berupa overview, guides, code snippets, serta responses code.</p>
          <p style="text-align: justify;"><strong>Bagaimana mengakses aplikasi pengujian Open API Pembayaran berbasis SNAP?</strong></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Untuk mengakses aplikasi pengujian, developer harus melakukan pendaftaran terlebih dahulu.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Pilih menu “Sign In”, masukan informasi yang diminta. Konfirmasi registrasi akan dikirimkan ke alamat email yang didaftarkan.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Setelah menerima konfirmasi, lakukan log in dengan user dan passwordyang telah didaftarkan.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Untuk meminta akses ke aplikasi pengujian, pilih menu “Request Aplikasi Pengujian” dan masukkan informasi yang diminta pada halaman tersebut (app name, app description) lalu pilih tombol “submit” untuk mengirimkan permintaan.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Permintaan akses tersebut akan muncul pada halaman “request” aplikasi pengujian.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Setelah permintaan akses aplikasi pengujian disetujui oleh pengelola SNAP Developer Site, developer akan memperoleh credentials yang diperlukan untuk melakukan pengujian.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Jika jangka waktu akses telah berakhir, developer dapat meminta perpanjangan akses ke aplikasi pengujian dengan memilih menu “request extend”.</p>
          <p style="text-align: justify;"><strong>Siapa yang dapat mendaftar pada Direktori Publikasi?</strong></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Para pihak yang telah mengembangkan Open API Pembayaran berbasis SNAP dan telah terverifikasi oleh pengelola SNAP dapat mengajukan pendaftaran pada Direktori Publikasi secara daring.</p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Untuk persyaratan verifikasi dan pihak yang melakukan verifikasi mengacu pada Peraturan Anggota Dewan Gubernur tentang Implementasi Standar Nasional Open API Pembayaran (peraturan tersebut dapat diakses pada&nbsp;<span style="color: #3598db;">www.POSyariah.co.id</span>&nbsp;).</p>
          <p style="text-align: justify;"><strong>Bagaimana mendaftar pada Direktori Publikasi?</strong></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Pilih menu “Direktori Publikasi”, masukkan informasi dan unggah dokumen yang diminta pada halaman tersebut.</p>
          <p style="text-align: justify;"><strong>Bagaimana melihat daftar para pihak yang telah memiliki Open API Pembayaran berbasis SNAP yang telah terverifikasi?</strong></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Pilih menu “Direktor Publikasi”, daftar para pihak dapat dipilih berdasarkan kategori alphabetical pada halaman tersebut.</p>
          <p style="text-align: justify;"><strong>Bagaimana jika ditemuakan tampilan SNAP Developer Site tidak tampil secara sempurna?</strong></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Pilih setting pada browser,kemudian lakukan clear cache pada browser</p>
          <p style="text-align: justify;"><em>Bagaimana menyampaikan pertanyaan terkait dengan standar teknis dan keamanan, standar data, dan spesifikasi teknis SNAP?</em></p>
          <p style="text-align: justify; padding-left: 40px;">•<span style="white-space: pre;"> </span>Kirimkan pertanyaan ke&nbsp;<span style="color: #3598db;">snap@POSyariah.co.id</span></p>
          <p style="text-align: justify;">&nbsp;</p>

          <b-modal
            id="sessionTimeout"
            ref="modal"
            title="Session timeout"
            ok-only
            @show="resetModal"
            @hidden="handleOKsessionTimeout"
            @ok="handleOKsessionTimeout"
          >
            <p class="my-4">Session Timeout, need relogin.</p>
          </b-modal>
          <b-modal
            id="notifResponse"
            ref="modal"
            title="Response result"
            ok-only
            @show="resetModal"
            @hidden="resetModal"
            @ok="handleOKnotifResponse"
          >
            <p class="my-4">Response from server: {{ response_error }}</p>
          </b-modal>
        </Widget>
      </div>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'
import backend from '@/server'
import Widget from '@/components/Widget/Widget';

export default {
  name: 'Home',
  components: {
    Widget
  },
  data() {
    return {
      model: {
      },
      loading: '',
      user_response: {},
      response_error: '',
    };
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      // this.post_users();
    },
    async post_users() {
      var url = backend.backendURI + '/api/v1/user'
      var token = window.localStorage.getItem('openapi-token')
      try {
        const resp = await axios.post(url, {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        });
        this.users_response = resp.data
        this.response_error = 'User Success'
        if (resp.status == 200) {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
      } catch (err) {
        this.response_error = err.response.data.remark
        if (err.response.status == 403) {
          this.$root.$emit("bv::show::modal", "sessionTimeout");
        } else {
          this.$root.$emit("bv::show::modal", "notifResponse");
        }
      }
    },
    handleOKsessionTimeout(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitsessionTimeout();
    },
    handleSubmitsessionTimeout() {
      this.$nextTick(() => {
        this.$router.push('/logout')
        this.$bvModal.hide('sessionTimeout');
      })
    },
    handleOKnotifResponse(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmitnotifResponse();
    },
    handleSubmitnotifResponse() {
      this.$nextTick(() => {
        this.$bvModal.hide('notifResponse');
      })
    },
  },
  computed: {
  }
};
</script>

<style src="./Home.scss" lang="scss" />
