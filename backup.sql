DROP DATABASE IF EXISTS Restaurante;
CREATE DATABASE Restaurante;

USE Restaurante;
SHOW TABLES;

SELECT * FROM universidade;
SELECT * FROM aluno;

INSERT INTO universidade (nome, cnpj, endereco)
VALUES ('Universidade Federal da Paraíba', '12.345.678/0001-90', 'Cidade Universitária, João Pessoa - PB');

INSERT INTO aluno (nome, usuario, senha, telefone, curso, matricula, email, universidade_id, bolsista, horario)
VALUES
('João Silva', 'joao.silva', 'abc1', '(83) 99999-1111', 'Ciência da Computação', '2020123456', 'joao.silva@exemplo.com', 1, 0, '{"segunda": ["08:00", "12:00"], "terça": ["13:00", "17:00"]}'),
('Maria Oliveira', 'maria.oliveira', 'abc2', '(83) 99999-2222', 'Engenharia Elétrica', '2020987654', 'maria.oliveira@exemplo.com', 1, 1, '{"quarta": ["08:00", "12:00"], "quinta": ["13:00", "17:00"]}'),
('Pedro Sousa', 'pedro.sousa', 'abc3', '(83) 99999-3333', 'Medicina', '2020112233', 'pedro.sousa@exemplo.com', 1, 2, '{"segunda": ["07:00", "11:00"], "sexta": ["19:00", "22:00"]}'),
('Ana Lima', 'ana.lima', 'abc4', '(83) 99999-4444', 'Direito', '2020456789', 'ana.lima@exemplo.com', 1, 0, '{"terça": ["13:00", "18:00"], "quinta": ["19:00", "22:00"]}'),
('Carlos Ferreira', 'carlos.ferreira', 'abc5', '(83) 99999-5555', 'Enfermagem', '2020554321', 'carlos.ferreira@exemplo.com', 1, 1, '{"segunda": ["07:00", "12:00"], "quarta": ["13:00", "18:00"]}'),
('Lucas Alves', 'lucas.alves', 'abc6', '(83) 99999-6666', 'Arquitetura', '2020789123', 'lucas.alves@exemplo.com', 1, 2, '{"quinta": ["07:00", "12:00"], "sexta": ["19:00", "22:00"]}'),
('Mariana Costa', 'mariana.costa', 'abc7', '(83) 99999-7777', 'Administração', '2020334455', 'mariana.costa@exemplo.com', 1, 0, '{"quarta": ["08:00", "12:00"], "sexta": ["13:00", "18:00"]}');