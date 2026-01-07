export default function Footer() {
  return (
    <footer style={styles.footer}>
      <p>© 2026 Smart Parking System</p>
      <p>Built with ❤️ using React & Django</p>
    </footer>
  );
}


const styles = {
  footer: {
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    color: "#fff",
    textAlign: "center",
    padding: "20px",
    marginTop: "40px"
  }
};
